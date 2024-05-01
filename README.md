The project relies on AI2-THOR, ProcTHOR-10k dataset and several LLMs: Llama3, Mistral and Gemma. Please pull them before running this code. The required versions are specified in ae_llm.py where more can be added, but currently the following versions are used: gemma:7b-instruct-v1.1-q6_K, mistral:7b-instruct-v0.2-q4_0, mistral:7b-instruct-v0.2-q6_K, llama3:8b-instruct-q6_K.

You must also install Thortils version from the referenced repository in the git submodule here. The vanilla Thortils will not work as I made several important changes. The best way to do that is to set up a conda environment for this purpose and install Thortils using:

```
git clone https://github.com/archie1983/llm_semantic_navigation
cd llm_semantic_navigation
git submodule init
git submodule update
cd thortils
pip install --no-cache-dir -e .
```

To demonstrate our approach, there are two main scripts:

extract_scene_data.py - for classifying a habitat from ProcTHOR-10k dataset. It will select next habitat with all 4 room types (Kitchen, Living room, Bedroom, Bathroom) from the training part of the dataset and then it will put the agent in random positions in that habitat and classify each random point belonging to a specific room- depending on objects observed around it.

semantic_path_planner.py - Uses the points classified by extract_scene_data.py to generate a path to an object of interest. It also plots the generated path on top of a top-view habitat image. I used this in the jupyter notebook "environment.ipynb" because running it from command line gave error: about xcb QT plugin that couldn't be started. I didn't have time to fix that, so ran it from jupyter notebook.

Finally analyse_classification_results.ipynb is where I analyzed test results and generated box plots.
generate_and_evaluate_datasets.ipynb is where I generated the SVC.
