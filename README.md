# PrefixLLM: LLM-aided Prefix Circuit Design

## Prerequisities

### Ubuntu
1. Download all required packages:

    Download this lib in python
    ```bash
    pip install -r requirements.txt
    ```

2. Config .yml files:
   ```bash
    Openai_API_Key -> your openai api key
    Model_Name -> selected openai model name (find your preferred model from this page https://platform.openai.com/docs/models)
    Level -> level limitation of prefix circuit
    BitWidth -> bit width of prefix circuit
    Spcr_It_Bound: the iteration bound of genrating a valid SPCR
    Dse_It_Bound: the iteration bound of our design exploration framework
    ```
   Note that for the model name, we recommend to select: o1 and o1-mini, which can derive the results using fewer iteration. If selecting other models such as gpt 4o, you may have to increase `Spcr_It_Bound` and `Dse_It_Bound`.

   

