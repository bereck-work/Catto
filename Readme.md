## Catto
Catto is a simple command line tool written in python that downloads random cute images of animals of your choice from the internet.
<img src="./gallery/catto_output.png" width=450px></img>

## Installation
Install the dependencies using the following command:
```bash
pip install -r requirements.txt
```
or if you are using poetry:
```bash
poetry install
```

## Usage
Catto has two modes of usage:
```bash
python -m catto download
```
This is argument based way of using catto.
For example, if you want to download a cat image, you can use the following command:
```bash
python -m catto download --category cats --amount 3 --path ./images
```
The above command will download 3 cat images and save them in the `./images` directory.

```bash
python -m catto interactive
```
Interactive mode is a fancy way to use catto. I can't explain it, only way to use it is to try it out.
To know more about catto run the following command:
```bash
python -m catto --help
```

## Typewriter effect
Typewriter effect prints the text in the terminal with a typewriter effect.
Catto allows you to disable / enable the typewriter effect at any time.

For example, if you want to disable the typewriter effect, you can use the following command:
```bash
python3 -m catto download --category cats --amount 3 --path ./images --typewriter False
```

Similarly, if you want to enable the typewriter effect, you can use the following command:
```bash
python3 -m catto download --category cats --amount 3 --path ./images --typewriter True
```

Typewriter effect can be enabled and disabled in interactive mode too.
```bash
python3 -m catto interactive --typewriter False
```

Typewriter mode is enabled by default.

## Note
The Readme.md file is not complete yet. I will add more content as I go.
