# PrefixLLM: LLM-aided Prefix Circuit Design

## Abstract
Prefix circuits are fundamental components in digital adders, widely used in digital systems due to their efficiency in calculating carry signals. Synthesizing prefix circuits with
minimized area and delay is crucial for enhancing the performance of modern computing systems. Recently, large language models (LLMs) have demonstrated a surprising ability to perform
text generation tasks. We propose PrefixLLM, that leverages LLMs for prefix circuit synthesis. PrefixLLM transforms the prefix circuit synthesis task into a structured text generation problem, termed the Structured Prefix Circuit Representation (SPCR), and introduces an iterative framework to automatically and accurately generate valid SPCRs. Furthermore, we present
a design space exploration (DSE) framework that uses LLMs to iteratively search for area and delay optimized prefix circuits. To further improve synthesis quality, we develop two enhancement techniques: simplification of prompt for SPCR generation, and a structural optimization heuristic. With these enhancements, PrefixLLM enables a general, non-reasoning LLM to achieve the same or even better performance as a powerful reasoning LLM, significantly reducing the deployment cost.

 <img width="558" align="center" alt="image" src="https://github.com/user-attachments/assets/a6c82f0d-cfc5-425c-a7af-e36d45798e38" />


## Usage
1. Download all required packages:

    Download this lib in python
    ```bash
    pip install -r requirements.txt
    ```

2. Config .yml files (`Config.yml`):

    (i) For the first version of our PrefixLLM (`USE_HUMAN_HEURISTIC`=0), only powerful reasoning LLMs can generate efficient prefix circuits, e.g., o1 and o1-mini. If selecting other general models such as gpt 4o, you may have to increase `Spcr_It_Bound` and `Dse_It_Bound`.
    
    (ii) For the current version of our PrefixLLM (`USE_HUMAN_HEURISTIC`=1), it supports general chatting LLMs to generate great prefix circuits, e.g., deepseek-V3.
    ```bash
    Openai_API_Key -> your openai api key
    DeepSeek_API_Key-> your deepseek api key
    Model_Name -> selected openai model name (find your preferred model from OpenAI (https://platform.openai.com/docs/models), DeepSeek (https://www.deepseek.com/), ...)
    Level -> level limitation of prefix circuit
    BitWidth -> bit width of prefix circuit
    Spcr_It_Bound: the iteration bound of genrating a valid SPCR
    Dse_It_Bound: the iteration bound of our design exploration framework
    USE_HUMAN_HEURISTIC: if set as 1, use our proposed enhanced techniques; else, our initial version of PrefixLLM 
    ```

3. Src files:

    ```bash
    PrefixCircuit.py -> Data structure definition of prefix circuit
    GeneratePrefixGPT_DepthLimit.py -> PrefixLLM methodology
    GenerateVerilog.py -> verilog generation script
    ```

4. Running PrefixLLM:

    ```bash
    python GeneratePrefixGPT_DepthLimit.py
    ```
    Note that for each time rerun `GeneratePrefixGPT_DepthLimit.py` without modifying `Config.yml`, you have to delete the corresponding output folder.

5. Results:

   GPTPrefix{`BitWidth`}_L{`Level`}: includes log files of each iteration during design space exploration

6. Example 1 (`BitWidth`=8, `Level`=4):

    <img width="607" alt="image" src="https://github.com/user-attachments/assets/88fcf8e1-3d79-4d3f-ad91-1c047ff99482" />

   Example 2 (`BitWidth`=16, `Level`=8):

   <img width="637" alt="image" src="https://github.com/user-attachments/assets/0270aa50-c35d-429b-9856-a7d17d769fc7" />




   

