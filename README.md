# TAC EDL 2019 Jig

This is the jig for the [Text Analysis Conference 2019 Entity Detection and Linking Task (TAC 2019 EDL)](http://nlp.cs.rpi.edu/kbp/2019/).  It is based on a setup for Dockerized IR experiments built for the [SIGIR 2019 Open-Source IR Replicability Challenge (OSIRRC 2019)](https://osirrc.github.io/osirrc2019/).

What's a [jig](https://en.wikipedia.org/wiki/Jig_(tool))?


To get started, clone the jig, and then download `neleval` (inside the `jig` directory) with the following command:

```
git clone https://github.com/wikilinks/neleval.git
```

Make sure the Docker Python package is installed (via pip, conda, etc.):
```
pip install -r requirements.txt
```

Make sure the Docker daemon is running.

Information on different datasets is in the directory `collections`.  A collection has three files:
 - `OntoNotes.txt`: explains what the collection is and where to get it from.
 - `OntoNotes.tree`: the output of [tree](http://mama.indstate.edu/users/ice/tree) on the collection directory.
 - `OntoNotes.md5`: MD5 checksums for files listed in the .tree file.

You will need to have the collection you want to use, laid out as described in the `.tree` file.

To test the jig with a simple demo image using default parameters, first obtain the sample Ontonotes data from http://nlp.cs.rpi.edu/kbp/2019/data.html.  Lay it out as in `collections/OntoNotes.tree`.  Then, try:

```
python run.py prepare \
    --repo isoboroff/edl-jig-test \
    --collections [name]=[path]=[format] ...
```

then

```
python run.py train \
    --repo isoboroff/edl-jig-test \
    --collection [name] \
    --train_split [path] \
    --validation_split [path] \
    --output /path/to/output
```

Change:
 - `[name]` and `[path]` to the collection name and path on the host, respectively
 - `/path/to/output` to the desired output directory.
 
The output run files will appear in the argument of `--output`.
The full command line parameters are below.

To run a container (from a saved image) that you can interact with, try:

```
python run.py interact \
    --repo isoboroff/edl-jig-test \
    --tag latest
```

## Collections

The following collections are supported:

|   Name      |                            URL                            |
|:-----------:|:---------------------------------------------------------:|
|  OntoNotes  |  http://nlp.cs.rpi.edu/kbp/2019/data.html                 |
|  FIGER      |  http://nlp.cs.rpi.edu/kbp/2019/data.html                 |
|  TAC 2019   |  LDC2019E79 (corpus) and LDC2019E78 (annotations)         |

## Command Line Options

Options with `none` as the default are required.

### Command Line Options - prepare

`python run.py prepare <options>`

| Option Name | Type | Default | Example | Description
| --- | --- | --- | --- | ---
| `--repo` | `string` | `none` | `--repo isoboroff/edl-jig-test` | the repo on Docker Hub
| `--tag` | `string` | `latest` | `--tag latest` | the tag on Docker Hub
| `--collections` | `[name]=[path]=[format] ...` | `none` | `--collections tac2019=/path/to/tac2019=tac ...` | the collections to use
| `--save_to_snapshot` | `string` | `save` | `--save_to_snapshot tac2019-exp1` | used to determine the tag of the snapshotted image after indexing
| `--opts` | `[key]=[value] ...` | `none` | `--opts index_args="-storeRawDocs"` | extra options passed to the index script
| `--version` | `string` | `none` | `--version 3b16584a7e3e7e3b93642a95675fc38396581bdf` | the version string passed to the init script

### Command Line Options - train

`python run.py train <options>`

| Option Name | Type | Default | Example | Description
| --- | --- | --- | --- | ---
| `--repo` | `string` | `none` | `--repo isoboroff/edl-jig-test` | the repo on Docker Hub
| `--tag` | `string` | `latest` | `--tag latest` | the tag on Docker Hub
| `--load_from_snapshot` | `string` | `save` | `--load_from_snapshot tac2019-exp1` | used to determine the tag of the snapshotted image to search from
| `--train_split` | `string` | `none` | `--train_split train_split` | the path to the file listing the files to use for training 
| `--validation_split` | `string` | `none` | `--validation_split valid_split` | the path to the file listing the files to use for the model validation
| `--gold` | `string` | `none` | `--gold annotations` | the path to annotations to use for model selection 
| `--model_folder` | `string` | `none` | `--model_folder $(pwd)/output` | the folder to save the model trained by the docker
| `--gpu` | `boolean` | `False` | `--gpu True` | flag to launch docker with nvidia runtime
| `--opts` | `[key]=[value] ...` | `none` | `--opts epochs=10` | extra options passed to the search script

### Command Line Options - test

`python run.py test <options>`

| Option Name | Type | Default | Example | Description
| --- | --- | --- | --- | ---
| `--repo` | `string` | `none` | `--repo isoboroff/edl-jig-test` | the repo on Docker Hub
| `--tag` | `string` | `latest` | `--tag latest` | the tag on Docker Hub
| `--collection` | `string` | `none` | `--collection tac2019` | the collections to index
| `--load_from_snapshot` | `string` | `save` | `--load_from_snapshot tac2019-exp1` | used to determine the tag of the snapshotted image to search from
| `--test_split` | `string` | `none` | `--test_split test_split` | the path to the file listing the files to use for testing
| `--gold` | `string` | `none` | `--gold annotations` | the path to annotations to use for evaluation 
| `--output` | `string` | `none` | `--output $(pwd)/output` | the output path for run files
| `--opts` | `[key]=[value] ...` | `none` | `--opts search_args="-bm25"` | extra options passed to the search script
| `--timings` | `flag` | `false` | `--timings` | print timing info (requires the `time` package, or `bash`, to be installed in Dockerfile)
| `--measures` | `string ...` | `"num_q map P.30"` | `--measures recall.1000 map` | the measures for trec_eval
| `--gpu` | `boolean` | `False` | `--gpu True` | flag to launch docker with nvidia runtime


### Command Line Options - interact
| Option Name | Type | Default | Example | Description
| --- | --- | --- | --- | ---
| `--repo` | `string` | `none` | `--repo osirrc2019/anserini` | the repo on Docker Hub
| `--tag` | `string` | `latest` | `--tag latest` | the tag on Docker Hub
| `--load_from_snapshot` | `string` | `save` | `--load_from_snapshot robust04-exp1` | used to determine the tag of the snapshotted image to interact with
| `--exit_jig` | `string` | `false` | `true` | determines whether jig exits after starting the container
| `--opts` | `[key]=[value] ...` | `none` | `--opts interact_args="localhost:5000"` | extra options passed to the interact script

# Docker Container Contract

Currently we support four hooks: `init`, `index`, `train`, `test`,and `interact`. We expect `train`; `test` or `interact` to be called after `init` and `index`. We also expect these five executables to be located in the root directory of the container.

Each script is executed with the interpreter determined by the shebang so you can use  `#!/usr/bin/env bash`, `#!/usr/bin/env python3`, etc - just remember to make sure your `Dockerfile` is built with the appropriate base image or the required dependencies are installed. 

### init
The purpose of the `init` hook is to do any preparation needed for the run - this could be downloading + compiling code, downloading a pre-built artifact, or downloading external resources (pre-trained models, knowledge graphs, etc.).

The script will be executed as `./init --json <json>`  where the JSON string has the following format:
```json5
{
  "opts": { // extra options passed to the init script
      "<key>": "<value>"
   }
}
```

### index
The purpose of the `index` hook is to build any indexes or other on-disk data structures required for the run.

Before the hook is run, we will mount the document collections at a path passed to the script.

The script will be executed as: `./index --json <json> ` where the JSON string has the following format:

```json5
{
  "collections": [
    {
      "name": "<name>",              // the collection name
      "path": "/path/to/collection", // the collection path
    },
    ...
  ],
  "opts": { // extra options passed to the index script
    "<key>": "<value>"
  },
}
```

### train
The purpose of the `train` hook is to train an EDL model.

The script will be executed as: `./train --json <json> ` where the JSON string has the following format:
```json5
{
  "collection": {
    "name": "<name>"          // the collection name
  },
  "train_split": {
    "path": "/path/to/split", // the path to the split file
  },
  "validation_split": {
    "path": "/path/to/split",  // the path to the split file
  },
  "model_folder": {
    "path": "/output",  // the path (in the docker image) where the output model folder (passed to the jig) is mounted
  },
  "opts": { // extra options passed to the train script
    "<key>": "<value>"
  },
}
```

### test
The purpose of the `test` hook is to perform an EDL run - multiple runs can be performed by calling `jig` multiple times with different `--opts` parameters.

The run files are expected to be placed in the `/output` directory such that they can be evaluated externally by `jig` using `trec_eval`.

The script will be executed as `./search --json <json>` where the JSON string has the following format:
```json5
{
  "collection": {
    "name": "<name>"          // the collection name
  },
  "opts": { // extra options passed to the search script
    "<key>": "<value>"
  },
  "test_split": {
    "path": "/path/to/split", // the path to the split file
  },
}
```

Note: If you're using the `--timings` option for the `test` hook, ensure that the `time` package (or `bash`) is installed in your `Dockerfile`.

### interact
The purpose of the `interact` hook is to prepare for user interaction, assuming that any process started by `init`, `index`, or `train` is gone.

The script will be executed as `./interact --json <json>` where the JSON string has the following format:
```json5
{
  "opts": { // extra options passed to the interact script
    "<key>": "<value>"
  },
}
```

Note: If you need a port accessible, ensure you `EXPOSE` the port in your `Dockerfile`.

## Azure Script

Run the script as follows:
`./azure.sh --disk-name <disk_name> --resource-group <group> --vm-name <vm_name> --vm-size <vm_size> --run-file <file.json> --ssh-pubkey-path <path> --subscription <id>`

The runs are defined in a JSON file, see `azure.json` as an example. Values in `[]` (i.e., `[COLLECTION_PATH]`) are replaced with the appropriate values defined in the file.

## Notes

Python 3.5 or higher is required to run `jig`.
Nvidia-docker is required to run images with gpu support, see https://github.com/NVIDIA/nvidia-docker for more details.
