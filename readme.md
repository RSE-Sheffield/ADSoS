## Installation
ADSoS has been tested with:

- Carla 0.9.15
- Python 3.8
- Ubuntu 24.04

### Prerequisites

- Carla 0.9.15
- Python 3.8

#### Python 3.8

Install the `pyenv` application via your package manager, e.g.

`sudo apt install pyenv`

Install Python 3.8 using pyenv:

`pyenv install 3.8`

Open a shell using Python 3.8:

`pyenv shell 3.8`

#### Carla
Set up and install [Carla 0.9.15](https://github.com/carla-simulator/carla/releases/tag/0.9.15) according to [its instructions](https://carla.readthedocs.io/en/latest/start_quickstart/)

### Installing ADSoS

Using git, clone the ADSoS repository:

`git clone git@github.com:MILeach/ADSoS-new.git`

Change directory into the ADSoS repository:

`cd ADSoS`

Pull in the PCLA submodule:

`git submodule update`

Set up PCLA according to [its instructions](https://github.com/MasoudJTehrani/PCLA#)

## Building the Documentation

### Building Documentation Locally

1. Run `mkdocs build`
2. The documentation will now be generated in the `site` directory, accessible by opening `index.html`

## Running the Examples

Four examples are available:

- **adsos_determinism_check.py** Runs the same vehicle configuration and scenario multiple times, logging the results and checking that there are no differences between the produced results
- **adsos_route_file_determinism.py** Runs the same vhicle configuration and scenario multiple times, loggin the results and checking that there are no differences between the produced results files. Equivalent to the above example, except this uses a supplied route file rather than spawn and end points for each ego vehicle
- **adsos_environment_matrix.py** Runs the same vehicle configuration with an automatically generated range of environmental conditions
- **adsos_random_search.py** Runs the same environment with multiple vehicle start/end point configurations. Each configuration is evaluated based on the minimum distance reached between any two ego vehicles and the 'best' configuration is reported