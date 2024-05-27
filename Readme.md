# Web Crawler

A simple web crawler implemented in Python. This web crawler starts from one or more seed URLs and recursively crawls web pages, obeying the `robots.txt` rules and rate limiting. It can store the crawled content and export the results to a text file.

## Features

- Recursively crawls web pages starting from seed URLs.
- Obeys `robots.txt` rules to respect website crawling policies.
- Allows setting a maximum crawl depth.
- Rate limits requests to avoid overwhelming servers.
- Supports specifying a custom `User-Agent` string.
- Saves crawled content and exports results to a text file.
- Prioritizes crawling the original domain before following external links.

## Requirements

- Python 3.6+
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/web-crawler.git
    cd web-crawler
    ```

2. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the crawler with the desired options:

```bash
python web_crawler.py [OPTIONS] URL [URL...]
```

### Command-Line Options

- `URL`: One or more seed URLs to start crawling from.

- `--max_depth`: (Optional) Maximum depth to crawl. This limits how deep the crawler will go when following links. Default is 3.
  
    ```bash
    --max_depth 3
    ```

- `--rate_limit`: (Optional) Time delay between requests in seconds. This helps in avoiding overloading the server. Default is 1 second.
  
    ```bash
    --rate_limit 1
    ```

- `--user_agent`: (Optional) User-Agent string to use for the HTTP requests. This can be useful to specify the crawler identity. Default is "MyCrawler".
  
    ```bash
    --user_agent "MyCustomCrawler"
    ```

- `--output_file`: (Optional) Output file to save the results. This specifies the path to the file where the crawled data will be stored. Default is "output.txt".
  
    ```bash
    --output_file results.txt
    ```

### Examples

1. Crawl a single website with default settings:

    ```bash
    python web_crawler.py https://example.com
    ```

2. Crawl multiple websites with a custom rate limit and user agent:

    ```bash
    python web_crawler.py https://example.com https://anotherexample.com --rate_limit 2 --user_agent "MyCustomCrawler"
    ```

3. Crawl a website and save results to a specified output file:

    ```bash
    python web_crawler.py https://example.com --output_file results.txt
    ```

## Example Output

```
             __                         __       
 _    _____ / /    ___________ __    __/ /__ ____
| |/|/ / -_) _ \  / __/ __/ _ `/ |/|/ / / -_) __/
|__,__/\__/_.__/  \__/_/  \_,_/|__,__/_/\__/_/   
                                                 

INFO:__main__:Crawling: https://example.com
INFO:__main__:Crawling: https://example.com/about
INFO:__main__:Crawling: https://example.com/contact
...
Crawling finished. Results saved to: output.txt
```

## Implementation Details

The crawler is implemented in the `web_crawler.py` script. Here's an overview of its components:

- **WebCrawler class**: Manages the crawling process, including fetching pages, parsing links, obeying `robots.txt`, and saving content.
- **print_banner()**: Prints a banner when the script starts.
- **main()**: Parses command-line arguments and initiates the crawling process.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
