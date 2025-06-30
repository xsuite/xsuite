import re
from collections import defaultdict
import matplotlib.pyplot as plt

# Expects files of the form "ipacYY.txt", where YY is the double-digit year, in the
# current directory. The files can be obtained from the PDF proceedings using
# e.g. the command `pdftotext proceedings.pdf ipacYY.txt`. The patterns in HEADERS
# aim to catch the doi that is given at the top of every page (and in this format
# pretty much only there). This may have to be adjusted for new files.

xsuite_mention = '[xX]-?(suite|track|fields|coll|wakes)'
madx_mention = 'MAD-X|MADX|madx|mad-x'
bmad_mention = 'BMAD|B-MAD|Bmad|BMad|bmad|b-mad'
elegant_mention = 'Elegant|ELEGANT'
madng_mention = 'MAD-NG|MADNG|madng|mad-ng'
rft_mention = 'RFTrack|RF-Track|RF-TRACK|RF-track|RFtrack|rf-track|rftrack|RfTrack'

PROGRAMS = {
    'Xsuite': xsuite_mention,
    'MAD-X': madx_mention,
    'Elegant': elegant_mention,
    'MAD-NG': madng_mention,
    'RF-Track': rft_mention,
    'BMAD': bmad_mention,
}

HEADERS = {
    25: 'doi: 10.18429/JACoW-IPAC25-(.*)',
    24: 'doi: 10.18429/JACoW-IPAC2024-(.*)',
    23: 'doi: 10.18429/JACoW-IPAC2023-(.*)',
    22: 'doi:10.18429/JACoW-IPAC2022-(.*)',
    21: 'doi:10.18429/JACoW-IPAC2021-(.*)',
}


def count(file, pattern, header_pattern):
    lines = open(file, 'r').readlines()

    # Count the mentions

    mentions = defaultdict(set)
    papers = defaultdict(set)
    all_papers = set()

    current_paper = None
    for line in lines:
        if match := re.search(header_pattern, line):
            current_paper = match.group(1)
            all_papers.add(current_paper)
        
        if match := re.search(pattern, line):
            pkg = match.group(0)
            
            if current_paper:
                mentions[current_paper].add(pkg)
                papers[pkg].add(current_paper)

    # Get the titles

    paper_pattern = '|'.join(mentions.keys())
    paper_toc_pattern = f'({paper_pattern}) [-–] (.*)'

    def trim_dots(string):
        i = len(string) - 1
        while string[i] == '.':
            i -= 1
        return string[:i + 1]

    title_for_code = {}

    for line in lines:
        if match := re.search(paper_toc_pattern, line):
            title_for_code[match.group(1)] = trim_dots(match.group(2))
    
    return mentions, papers, title_for_code, all_papers


dataset = defaultdict(dict)

for year, header_pattern in HEADERS.items():
    for program, program_pattern in PROGRAMS.items():
        mentions, papers, title_for_code, all_papers = count(f'ipac{year}.txt', program_pattern, header_pattern)
        dataset[program][year] = len(mentions.keys()) / len(all_papers)

for program, values in dataset.items():
    years = list(values.keys())
    ratios = list(values.values())
    plt.plot(years, ratios, label=program, marker='.', linestyle='-')

plt.xticks(list(HEADERS.keys()))
plt.title('Ratio of IPAC papers mentioning software tools by year')
plt.legend()
plt.show()
