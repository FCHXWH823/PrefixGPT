# PrefixLLM: LLM-aided Prefix Circuit Design

1. Download all required packages:

    Download this lib in python
    ```bash
    pip install -r requirements.txt
    ```

2. Config .yml files (`Config.yml`):
    Note that for the model name, we recommend to select: o1 and o1-mini, which can derive the results using fewer iteration. If selecting other models such as gpt 4o, you may have to increase `Spcr_It_Bound` and `Dse_It_Bound`.
    ```bash
    Openai_API_Key -> your openai api key
    Model_Name -> selected openai model name (find your preferred model from https://platform.openai.com/docs/models)
    Level -> level limitation of prefix circuit
    BitWidth -> bit width of prefix circuit
    Spcr_It_Bound: the iteration bound of genrating a valid SPCR
    Dse_It_Bound: the iteration bound of our design exploration framework
    ```
    Note that for the model name, we recommend to select: o1 and o1-mini, which can derive the results using fewer iteration. If selecting other models such as gpt 4o, you may have to increase `Spcr_It_Bound` and `Dse_It_Bound`.

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

6. Example (`BitWidth`=8, `Level`=4):
    <img width="607" alt="image" src="https://github.com/user-attachments/assets/88fcf8e1-3d79-4d3f-ad91-1c047ff99482" />



   

