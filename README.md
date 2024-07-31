# IA Downloader

Welcome to IA Downloader! This nifty tool lets you dive into the vast sea of files on the Internet Archive. Simply enter an Identifier, and we'll fetch all the goodies for you. Sit back and relax as we handle the technical stuff while you enjoy the show. Download speeds may vary based on the archive's mood!

## Features

- **Easy to Use**: Just enter the Identifier of the Internet Archive item, and the tool does the rest.
- **Asynchronous Downloads**: Utilizes `aiohttp` for efficient and fast downloading.
- **Progress Bars**: Provides visual feedback on download progress with `tqdm`.
- **Automatic Jokes**: Keeps you entertained with periodic jokes during long downloads.

## Prerequisites

- Python 3.6+
- `aiohttp` library
- `tqdm` library

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Ghosty-Tongue/IA-Downloader.git
   cd IA-Downloader
   ```

2. Install the required libraries:
   ```sh
   pip install aiohttp tqdm
   ```

## Usage

1. Run the script:
   ```sh
   python iadownloader.py
   ```

2. Enter the Identifier of the Internet Archive item when prompted.

3. Follow the on-screen instructions to download the desired files.

## Example

```sh
Enter the Identifier of the Internet Archive item (or 'exit' to quit): example-identifier
Total size of all files: 1.23 GB

Available files:
1. file1.txt
2. file2.mp4
3. file3.pdf
4. Download all files

Enter the number of the file you want to download (or the number to download all files): 4
Downloading all files... Let the download fiesta begin!
```

## Contributing

Feel free to fork this repository, make enhancements, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Contact

Developed by GhostyTongue. For any inquiries, please reach out via [GitHub Issues](https://github.com/Ghosty-Tongue/IA-Downloader/issues).
