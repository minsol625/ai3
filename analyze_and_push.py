import os
import re
import subprocess
from collections import Counter

def extract_keywords_from_file(file_path):
    """파일에서 큰따옴표 안의 키워드를 추출합니다."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    dialogues = re.findall(r'"(.*?)"', content)  # 큰따옴표 안의 텍스트 찾기
    words = []
    for dialogue in dialogues:
        words.extend(re.findall(r'\b\w+\b', dialogue))  # 단어 단위로 분리
    return Counter(words)

def analyze_repository(repo_path, output_file):
    """리포지토리 내 모든 .txt 파일을 분석하여 결과를 저장합니다."""
    total_counter = Counter()
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                total_counter += extract_keywords_from_file(file_path)
    
    # 결과를 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("Keyword Frequency Analysis\n")
        out.write("===========================\n")
        for word, count in total_counter.most_common(20):  # 상위 20개 키워드
            out.write(f"{word}: {count}\n")
    print(f"Analysis saved to {output_file}")

def git_commit_and_push(repo_path, commit_message):
    """Git 명령어를 사용해 결과 파일을 GitHub에 업로드합니다."""
    try:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
        subprocess.run(["git", "push"], cwd=repo_path, check=True)
        print("Changes committed and pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")

if __name__ == "__main__":
    # 리포지토리 경로 입력받기
    repo_path = input("Enter the path to the GitHub repository: ").strip()
    output_file = os.path.join(repo_path, "keyword_analysis.txt")  # 결과 파일 이름
    
    # 키워드 분석 및 결과 저장
    analyze_repository(repo_path, output_file)
    
    # GitHub에 결과 파일 업로드
    commit_message = "Add keyword analysis results"
    git_commit_and_push(repo_path, commit_message)
