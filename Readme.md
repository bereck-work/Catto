## Catto
Catto is a simple command line tool written in python that downloads random cute images of animals of your choice from the internet.
<img src="./gallery/catto_output.png" width=450px></img>

## Installation
To install catto, run the following command:
```
git clone https://github.com/KortaPo/Catto.git
```

Install the dependencies using the following command:
```bash
pip3 install -r requirements.txt
```
or if you are using poetry:
```bash
poetry install
```

## Usage
Catto has two modes of usage:
```bash
python3 -m catto download
```
This is argument based way of using catto.
For example, if you want to download a cat image, you can use the following command:
```bash
python3 -m catto download --category cats --amount 3 --path ./images
```
The above command will download 3 cat images and save them in the `./images` directory.

```bash
python3 -m catto interactive
```
Interactive mode is a fancy way to use catto. I can't explain it, but you can try it out.

To know more about catto run the following command:
```bash
python3 -m catto --help
```
## Note
The Readme.md file is not complete yet. I will add more content as I go.
