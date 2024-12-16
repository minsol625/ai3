import os
import re
import subprocess
from collections import Counter

def extract_keywords_from_file(file_path):
    """파일에서 큰따옴표 안 키워드 추출"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    dialogues = re.findall(r'"(.*?)"', content)
    words = []
    for dialogue in dialogues:
        words.extend(re.findall(r'\b\w+\b', dialogue))  
    
    return Counter(words)

def analyze_repository(repo_path, output_file):
    total_counter = Counter()
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                total_counter += extract_keywords_from_file(file_path)
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("Keyword Frequency Analysis\n")
        out.write("===========================\n")
        for word, count in total_counter.most_common(20):
            out.write(f"{word}: {count}\n")
    print(f"Analysis saved to {output_file}")

def git_commit_and_push(repo_path, commit_message):
    try:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
        subprocess.run(["git", "push"], cwd=repo_path, check=True)
        print("Changes committed and pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")

if __name__ == "__main__":
    repo_path = input("Enter the path to the GitHub repository: ").strip()
    output_file = os.path.join(repo_path, "keyword_analysis.txt")
    
    analyze_repository(repo_path, output_file)
    
    commit_message = "Add keyword analysis results"
    git_commit_and_push(repo_path, commit_message)
