<h3 align="center">Extracting PDFs of Authors</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Few lines describing your project.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Built Using](#built_using)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [TODO](#todo)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>

Tool to obtain list of papers of interested profs from a CSV and parse PDFs into text for creating embeddings and query with GPT

### Built using <a name = "built_using"></a>

- SerpAPI
- PyPDF2
- OpenAI GPT 3
- Tiktoken

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisites

- One needs to have an account with SerpAPI [https://serpapi.com/]. SerpAPI is used to query Google Scholar, and it allows upto 100 free queries per month.

- Additionally, one needs access to OpenAI GPT APIs [https://platform.openai.com/account/api-keys].

Create a `config.yaml` file with the following keys:

```
csv: <CSV FILE NAME>
serpapi_key: <SerpAI API_KEY>
openai:
  api_key: <OpenAI API_KEY>
  organization: <Org name registered with OpenAI>

```

### Installing

Create the environment

`conda env create -f environment.yml`

## 🎈 Usage <a name="usage"></a>

To fetch all papers from 2022 onwards of profs of interest:
`python fetch.py`

This should create a folder `papers` which contain the PDFs

Then to extract data from PDFs run

`python extract.py`

This should create a folder `papers_parse` which contain the parsed data from each PDF

Finally, to ask a question from GPT run

`python gpt.py -question <QUESTION> -new <True/False>`

Set the `-new` flag to `True` if one wants to create new embeddings. Else set to `False`.

## TODO <a name="todo"></a>

- Instead of using PyPDF, use Grobid [https://huggingface.co/spaces/kermitt2/grobid] for better PDF parsing
- Finetune GPT model

## ✍️ Authors <a name = "authors"></a>

- [@saksham36](https://github.com/saksham36)
