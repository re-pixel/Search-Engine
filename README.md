# PDF Search Engine

A Python-based search engine for PDF documents that implements advanced data structures (Trie and Graph) to provide fast and intelligent search capabilities with features like autocomplete, spell correction, and PageRank-style relevance ranking.

## Features

- **Fast Text Search**: Uses a Trie data structure for efficient word lookup
- **Boolean Queries**: Support for AND, OR, and NOT operators
- **Autocomplete**: Wildcard search with intelligent suggestions
- **Spell Correction**: "Did you mean?" suggestions for misspelled queries
- **Relevance Ranking**: Pages ranked by keyword frequency and cross-reference importance
- **Result Highlighting**: Search terms are highlighted in context
- **PDF Generation**: Creates a PDF with the top 10 search results
- **Interactive Results**: Browse through results with pagination

## Requirements

- Python 3.x
- PyMuPDF (pymupdf)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/re-pixel/Search-Engine.git
cd Search-Engine
```

2. Install dependencies:
```bash
pip install pymupdf
```

3. Place your PDF document:
   - The default PDF path is `"Data Structures and Algorithms in Python.pdf"`
   - You can change this by modifying the `pdf_path` variable in `main.py`

4. Initialize the search index:
   - On first run, you'll need to generate the index files
   - The program will create a `serialized/` directory with three files:
     - `text.pkl`: Extracted text from the PDF
     - `trie.pkl`: Trie data structure for word search
     - `graph.pkl`: Graph structure for page references

   To generate these files, you need to run the indexing functions first (uncomment and run the generation code in `main.py`):
   ```python
   # Generate index (run once)
   text = extract_text_from_pdf(pdf_path)
   trie = generate_trie(text)
   graph = generate_graph(references)
   ```

## Usage

Run the search engine:
```bash
python main.py
```

### Search Syntax

1. **Simple Search**: Enter a single word or multiple words
   ```
   algorithm
   data structure
   ```

2. **Boolean Search**: Use AND, OR, NOT operators
   ```
   algorithm AND tree
   sorting OR searching
   array NOT linked
   ```

3. **Complex Queries**: Use parentheses for grouping
   ```
   (algorithm OR data) AND structure
   tree AND (binary OR search)
   ```

4. **Autocomplete**: Add asterisk (*) at the end for suggestions
   ```
   algo*
   ```
   This will display up to 3 suggestions based on popularity.

### Example Session

```
Pretrazite pdf dokument: algorithm*
1. algorithm
2. algorithms
3. algorithmic
Izaberite opciju: 1

Results will show matching pages with highlighted terms...
```

## Project Structure

```
Search-Engine/
├── main.py           # Main application with search logic
├── trie.py          # Trie data structure implementation
├── graph.py         # Graph data structure for page references
├── serialized/      # Directory for index files (generated)
│   ├── text.pkl     # Extracted PDF text
│   ├── trie.pkl     # Trie index
│   └── graph.pkl    # Reference graph
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

## How It Works

### Data Structures

1. **Trie (Prefix Tree)**
   - Stores all words from the PDF for efficient prefix-based search
   - Each node tracks word frequency and page locations
   - Enables O(m) search time where m is the word length

2. **Graph**
   - Tracks cross-references between pages
   - Uses incoming/outgoing edges to model page relationships
   - Implements a PageRank-like algorithm for relevance scoring

### Search Algorithm

1. **Query Parsing**: Breaks down complex boolean queries
2. **Word Lookup**: Uses Trie to find pages containing each term
3. **Set Operations**: Applies AND/OR/NOT operations on result sets
4. **Ranking**: Scores pages based on:
   - Keyword frequency
   - Number of references to the page
   - Relevance of referring pages
5. **Result Generation**: Creates PDF with top results and displays formatted output

### Spell Correction

The system uses frequency-based heuristics to suggest corrections:
- Identifies the longest valid prefix in the query
- Suggests the most popular words with that prefix

## Output

- **Console**: Displays paginated search results with context snippets
- **PDF File**: `search_results.pdf` contains the top 10 matching pages

## Limitations

- Currently optimized for "Data Structures and Algorithms in Python" PDF
- Page number references are offset by 21 (specific to the source PDF)
- Maximum word length for indexing is 20 characters
- Phrase search is not yet implemented (commented out in code)

## Future Enhancements

- [ ] Phrase search support
- [ ] Multiple PDF document support
- [ ] GUI interface
- [ ] Export results to multiple formats
- [ ] Advanced filtering options
- [ ] Configurable ranking weights

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Authors

- [re-pixel](https://github.com/re-pixel)

## Acknowledgments

This project was built as a demonstration of applying data structures and algorithms to real-world problems.
