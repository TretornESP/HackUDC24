# How to manage Codee 

We will execute the codee following the [Quickstart guide](https://www.codee.com/wp-content/uploads/2023/02/Codee-Quickstart-CMake.pdf).

## Step 1: Understand how to use Codee over mbedtls

First we will get into the repository:

```bash
cd mbedtls
```

Then we will **take advantage of Codee integration with CMake** by producing the
compile commands database in JSON format:

```bash
cmake -DCMAKE_C_COMPILER=gcc -DCMAKE_EXPORT_COMPILE_COMMANDS=On -DCMAKE_BUILD_TYPE=Release -B build -G "Unix Makefiles" ./
make -C build
```

This will generate a `compile_commands.json` file in the `build` directory. 

Then, we will use Codee to analyze the code. First, we will run a screening phase.

```bash
pwreport ./* --config build/compile_commands.json --screening --lang C --show-progress
```

We will use:
 - The `--config` flag to specify the compile commands database.
 - The `--screening` flag to run the screening phase.
 - The `--lang` flag to specify the language of the code.
 - The `--show-progress` flag to see the progress of the analysis.

After the screening phase, we will run the checking phase.

```bash
pwreport ./* --config build/compile_commands.json --checks --verbose --lang C --show-progress
```

We will use:
 - The `--config` flag to specify the compile commands database.
 - The `--checks` flag to run the checking phase.
 - The `--verbose` flag to get more detailed information about the issues found.
 - The `--lang` flag to specify the language of the code.
 - The `--show-progress` flag to see the progress of the analysis.


## Step 2: Obtain Codee metrics for chart generation
When new changes are commited into the repository, a new worker container is instantiated to execute Codee and obtain the possible optimizations that can be applied in the code.

Initially, the repository is cloned into the container and the compile commands database is produced for the Codee execution.
The script then executes 2 commands of CODEE to obtain the maximum amount of available information:
```bash
pwreport ./* --config build/compile_commands.json --screening --lang C --json --exclude build/
pwreport ./* --config build/compile_commands.json --checks --verbose --lang C --json --exclude build/
``` 
Information about the repository and the last commit is also collected.
A Json file containing the information from Codee and from the last commit applied to the repository is created and forwarded to a web-server to store and use in future report generation. 

