"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from __future__ import print_function

import sys

from utils import logger

try:
    if hasattr(sys, '_run_from_cmdl') is True:
        raise ImportError
    from pycompss.api.parameter import FILE_IN, FILE_OUT
    from pycompss.api.task import task
    from pycompss.api.api import compss_wait_on
except ImportError:
    logger.warn("[Warning] Cannot import \"pycompss\" API packages.")
    logger.warn("          Using mock decorators.")

    from utils.dummy_pycompss import FILE_IN, FILE_OUT  # pylint: disable=ungrouped-imports
    from utils.dummy_pycompss import task  # pylint: disable=ungrouped-imports
    from utils.dummy_pycompss import compss_wait_on  # pylint: disable=ungrouped-imports

from basic_modules.tool import Tool
from basic_modules.metadata import Metadata

# ------------------------------------------------------------------------------


class chasTool(Tool):  # pylint: disable=invalid-name
    """
    Tool for writing to a file
    """

    def __init__(self, configuration=None):
        """
        Init function
        """
        logger.info("Test writer")
        Tool.__init__(self)

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)

    @task(returns=bool, file_in_loc=FILE_IN, file_out_loc=FILE_OUT, isModifier=False)
    def test_writer(self, matrix_file, features_file, file_out_loc, file_out_targz):  # pylint: disable=no-self-use
        """
        Count the number of characters in a file and return a file with the count

        Parameters
        ----------
        matrix_file: str
            Location of the input matrix file
        feaures_file: str
            Location of the input features file
        file_out_loc : str
            Location of an output file

        Returns
        -------
        bool
            Writes to the file, which is returned by pyCOMPSs to the defined location
        """

        from subprocess import check_output, CalledProcessError

        try:
            import os
            tool_path = os.path.dirname(os.path.abspath(__file__))
            print('Rscript '+ tool_path + '/../../ChAs/ChAs_basic.R')
            with open(file_out_loc,'w') as results_file:
                # Run ChAs for all the network
                logger.info('Processing all chromosomes together first')
                cmd = ' '.join(['Rscript '+ tool_path + '/../../ChAs/ChAs_basic.R', matrix_file, features_file])
                output = check_output(cmd, shell=True)
                header, values = output.rstrip().split('\n')
                # Move header one colum to right
                header = header.split('\t')
                header.insert(0,'')
                # Insert chromosome number as the first column value, in this case 'ALL'
                values = values.split('\t')
                values[0] = 'ALL'

                results_file.write('\t'.join(header))
                results_file.write('\n')
                results_file.write('\t'.join(values))
                results_file.write('\n')

                # Chromosome list
                chromosomes = list(map(lambda c: str(c), list(range(1, 20))))
                chromosomes += ['X', 'Y']
                for chromosome in chromosomes:
                    logger.info('Processing chromosome ' + chromosome)
                    cmd = ' '.join(['Rscript '+ tool_path + '/../../ChAs/ChAs_basic.R', matrix_file, features_file, chromosome])
                    output = check_output(cmd, shell=True)
                    header, values = output.rstrip().split('\n')
                    values = values.split('\t')
                    # Use the chromosome number as the first value of the row
                    values[0] = chromosome
                    results_file.write('\t'.join(values))
                    if chromosome != 'Y':
                        results_file.write('\n')

            logger.info('Tar the output results')
            check_output("tar cf " + file_out_targz + " -C " + self.configuration['execution'] + " $(basename " + file_out_loc + ")" , shell=True)

        except CalledProcessError as error:
            logger.fatal("error({0})".format(error))
            return False

        return True

    def run(self, input_files, input_metadata, output_files):
        """
        The main function to run the test_writer tool

        Parameters
        ----------
        input_files : dict
            List of input files - In this case there are no input files required
        input_metadata: dict
            Matching metadata for each of the files, plus any additional data
        output_files : dict
            List of the output files that are to be generated

        Returns
        -------
        output_files : dict
            List of files with a single entry.
        output_metadata : dict
            List of matching metadata for the returned files
        """
	if not output_files["output"]:
            output_files["output"] = self.configuration['execution'] + '/dinamic_name.tsv'

        results = self.test_writer(
            input_files["matrix"],
            input_files["features"],
            output_files["output"],
            output_files["output_tar"]
        )
        results = compss_wait_on(results)

        if results is False:
            logger.fatal("Test Writer: run failed")
            return {}, {}

        output_metadata = {
            "output": Metadata(
                #data_type="<data_type>",
                #file_type="txt",
                file_path=output_files["output"],
                sources=[input_metadata["matrix"].file_path, input_metadata["features"].file_path],
                taxon_id=input_metadata["matrix"].taxon_id,
                meta_data={
                    "tool": "ChAs"
                }
            ),
            "output_tar": Metadata(
                #data_type="<data_type>",
                #file_type="txt",
                file_path=output_files["output"],
                sources=[input_metadata["matrix"].file_path, input_metadata["features"].file_path],
                taxon_id=input_metadata["matrix"].taxon_id,
                meta_data={
                    "tool": "ChAs"
                }
            )
        }

        return (output_files, output_metadata)
