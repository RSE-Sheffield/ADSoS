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

### Changing PCLA version

- **Pulling in Changes** to pull changes from the remote, run the command `git submodule update --remote`
- **Changing the remote repo** 
    1. Navigate into the submodule repo `cd PCLA`
    2. Remove the old remote `git remote remove origin`
    3. Add the new remote `git remote add origin [link to git repo]`
    4. Update `git submodule update --remote`
- **Syncing a fork on github**
    1. Navigate to your fork in the web browser
    2. Click the `Sync Fork` button
    3. Click `Update Branch`


### Running the Examples

Four examples are available:

- **adsos_determinism_check.py** Runs the same vehicle configuration and scenario multiple times, logging the results and checking that there are no differences between the produced results
- **adsos_route_file_determinism.py** Runs the same vhicle configuration and scenario multiple times, loggin the results and checking that there are no differences between the produced results files. Equivalent to the above example, except this uses a supplied route file rather than spawn and end points for each ego vehicle
- **adsos_environment_matrix.py** Runs the same vehicle configuration with an automatically generated range of environmental conditions
- **adsos_random_search.py** Runs the same environment with multiple vehicle start/end point configurations. Each configuration is evaluated based on the minimum distance reached between any two ego vehicles and the 'best' configuration is reported

## Building the Documentation

### Building Documentation Locally

1. Run `mkdocs build`
2. The documentation will now be generated in the `site` directory, accessible by opening `index.html`

### Pushing Updated Documentation to github

Running the command `mkdocs gh-deploy` will automatically build the documentation, commit it to the gh-pages branch and push it to github.

## Using ADSoS

### Structure of an ADSoS Simulation
All ADSoS programs will follow a similar structure.

1. Initialise the client and connect to Carla
2. Specify ego vehicle configuration
3. Construct a `runner` which will be responsible for mutating the simulation between runs and controlling the simulation execution
4. Supply initial configuration and specify how the simulation should change on each iteration

### Initialising the client and connecting to Carla
At the start of our program we must connect to the Carla server

    def main():
    
        # Connect to the Carla server
        HOST_IP: str = "localhost"
        client = carla.Client(HOST_IP, 2000)
        client.set_timeout(10.0)
        client.load_world("Town02")

### Ego Vehicle Configuration

Ego vehicles are specified as a list of `ADSoSVehicleConfiguration` objects. These are constructed using a vehicle model name, an ADS name and either a spawn and end point id, or a route file and route id.

    # Add some vehicles using spawn/end points
    vehicles = [
        ADSoSVehicleConfiguration('model3', "carl_carl_0", spawn_point_id=31, end_point_id=11),
        ADSoSVehicleConfiguration('model3', "carl_carl_1", spawn_point_id=27, end_point_id=14)
    ]
    
#### Supported ADS names:

**SimLingo**

-   Also known as CarLLava.

-   `simlingo_simlingo`: The best-performing agent, which secured **first place** at [CARLA Leaderboard 2](https://leaderboard.carla.org) SENSORS track (previously named CarLLava).
        

**LMDrive**

-   `lmdrive_llava`: Best performing LMDrive agent.
        
-   `lmdrive_vicuna`: Second best performing LMDrive agent.
        
-   `lmdrive_llama`: Third best performing LMDrive agent.
        

**TransfuserV3**

-   Also known as Transfuser. See [the history of Transfuser](https://ln2697.github.io/lead/docs/transfuser_versions.html).

-   `tfv3_tf`: The main Transfuser agent.
        
-   `tfv3_ltf`: The LatentTF agent.
        
-   `tfv3_lf`: The Late_Fusion agent.
        
-   `tfv3_gf`: The Geometric_Fusion agent.
        

**TransfuserV4**

-   Also know as Transfuser++ for Leaderboard 1.

-   **Seeds:** Replace `#` with the seed number from **0 to 2** (e.g., `tfpp_l6_0`).
        
-   `tfv4_l6_#`: Best performing Transfuser++ agent. Second place at CARLA Leaderboard 2 SENSORS track.
        
-   `tfv4_lav_#`: Transfuser++ not trained on Town02 and Town05.
        
-   `tfv4_wp_#`: Transfuser++ WP from their paper's appendix.
        
-   `tfv4_aim_#`: Reproduction of the [AIM](https://openaccess.thecvf.com/content/CVPR2021/html/Prakash_Multi-Modal_Fusion_Transformer_for_End-to-End_Autonomous_Driving_CVPR_2021_paper.html) method.
        
**TransfuserV5**

-   Also known as Transfuser++ for Leaderboard 2. This version has a bit of similar performance as TransfuserV4

-   `tfv5_alltowns`: This agent is trained with all towns.

-   `tfv5_notown13`: This agent is trained excluding Town13.

**TransfuserV6**

-   The most recent Transfuser agent, also known as Lead.

-   `tfv6_regnet`: Their best-performing agent that uses regnety032.

-   `tfv6_resnet`: The second-best-performing agent that uses resnet34.

-   `tfv6_4cameras`: Uses 4cameras and resnet34.

-   `tfv6_noradar`: Uses resnet34 but no radar sensor.

-   `tfv6_visiononly`: Vision-only driving model and resnet34.

-   `tfv6_notown13`: Uses resnet34 but Town13 is excluded.

**CaRL**

-   `carl_carl_#`: CaRL agent with a driving score of 64. Replace `#` with **0 or 1**.
        
-   `carl_carlv11`: The best CaRL agent with a driving score of 73. Best open-source RL planner on longest6 v2 and nuPlan.


**Roach**

-   `carl_roach_#`: The Roach planner agent ([paper](https://arxiv.org/abs/2108.08265)) reproduced by the authors of [CaRL](https://github.com/autonomousvision/CaRL/tree/main). Replace `#` with a number from **0 to 4** for the 5 available seeds.


**PlanT**

-   `carl_plant_#`: The PlanT planner agent ([paper](https://arxiv.org/abs/2210.14222)) reproduced by the authors of [CaRL](https://github.com/autonomousvision/CaRL/tree/main). Replace `#` with a number from **0 to 4** for the 5 available seeds.

**PlanT 2**

-   `plant2_plant2_#`: The PlanT 2.0 agent. Replace `#` with a number from **0 to 2** for the 3 available seeds.

**NEAT**
  
-   `neat_neat`
        
-   `neat_aimbev`
        
-   `neat_aim2dsem`
        
-   `neat_aim2ddepth`


**Interfuser**
 
-   `if_if`: Second best performing [CARLA Leaderboard 1](https://leaderboard.carla.org) SENSORS track agent.

**Learning from All Vehicles (LAV)**

-   `lav_lav`: The original LAV agent.
        
-   `lav_fast`: Leaderboard submission optimized for inference speed with temporal LiDAR scans.
        

**Learning By Cheating (LBC)**

-   `lbc_nc`: Learning By Cheating, the NoCrash model.
        
-   `lbc_lb`: Learning By Cheating, the Leaderboard model.
        

**World on Rails (WoR)**

-   `wor_nc`: World on Rails, the NoCrash model.
        
-   `wor_lb`: World on Rails, the Leaderboard model.

### Creating a Runner
Runners are objects which will manage your simulation instances. The provided runners are capable of searching a set of vehicle configurations (`RandomSearchRunner`) or environment configurations (`EnvironmentMatrixRunner`), or checking for determinism within repeated runs of the same configuration (`DeterminismRunner`). You can also create your own runners if you need further functionality. 

Some runners require additional configuration objects. This example will show how to set up a `RandomSearchRunner`. The `RandomSearchRunner` requires an `EvaluationStrategy`, and can optionally have multiple `EndConditions`. The runner will continue until one of the end conditions is met.

First, we choose an evaluation strategy. The `EgoMinimumDistanceEvaluationStrategy` scores the scenario according to the minimum distance reached between any two ego vehicles during the simulation:

    evaluation_strategy = EgoMinimumDistanceEvaluationStrategy()
    evaluator = ScenarioEvaluator(evaluation_strategy)
    
We then specify an end condition. The `NumSearchesEndCondition` will trigger after a fixed number of trial configurations have been used. In this case, we will search 15 trial configurations.

    end_condition = NumSearchesEndCondition(15)
    
We can now construct, configure and run our `RandomSearchRunner` object.

    runner = RandomSearchRunner(client=client, steps=150, evaluator=evaluator)
    runner.set_initial_vehicle_configuration(vehicles=vehicles)
    runner.add_end_condition(end_condition)
    runner.run()
    runner.write("search_results.json")

## Extending ADSoS

ADSoS objects can be extended to add custom functionality.

### Creating Your Own End Condition

Custom end conditions can be created by extending the `SearchEndCondition` base class which is defined as shown below:

    class SearchEndCondition(ABC):
        def __init__(self):
            self.runner = None
            
        def set_search_runner(self, runner):
            self.runner = runner
            
        @abstractmethod
        def is_condition_met(self) -> bool:
            pass
            
The `set_search_runner` method is automatically called when an `EndCondition` is added to a `Runner`, so all that is really required to add a new condition is to extend this class and override the `is_condition_met` method. This method is automatically called at the end of each scenario run and should return true when the condition is triggered and the simulation should end. As an example, to create a new end condition which triggers when a scenario is found with an evaluation score above a given threshold, we could do the following:

    from runners.search.end_conditions.search_end_condition import SearchEndCondition
    
    class ThresholdScoreEndCondition(SearchEndCondition):
        def __init__(self, threshold_score: int):
            super().__init__()
            self.threshold_score = threshold_score
            
        def is_condition_met(self):
            return self.runner.results[-1][0] >= self.threshold_score
            
### Creating Your Own Evaluation Strategy
Evaluation strategies give a score to a simulation run. They inherit from the `ScenarioEvaluationStrategy` class which is defined as:

    class ScenarioEvaluationStrategy(ABC):
        def __init__(self):
            self.scores: List[float] = []
    
        @abstractmethod
        def evaluate_frame(self, world, ego_vehicles: List[PCLA]) -> float:
            pass
            
        def get_scores(self) -> List[float]:
            return self.scores
    
        def reset(self) -> None:
            self.scores = []
            
The `evaluate_frame` method is called at the end of each simulation step and should be overridden to return a score. The `ScenarioEvaluator` object will aggregate the per-frame scores to produce a final score for the scenario configuration.