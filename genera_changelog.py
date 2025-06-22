import subprocess
import sys

def get_commit_info(commit_hash):
    try:
        author = subprocess.check_output(
            ['git', 'show', '-s', '--format=%an', commit_hash],
            text=True
        ).strip()

        message = subprocess.check_output(
            ['git', 'show', '-s', '--format=%B', commit_hash],
            text=True
        ).strip().split(':')[-1].strip()

        return author, message

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)


def update_changelog(changelog_file, author, message, commit_hash):
    with open(changelog_file, 'a', encoding='utf-8') as f:
        f.write(f"- **{author}**: {message}. Commit: `{commit_hash}`\n")


if __name__ == "__main__":
    commit_hash = sys.argv[1]
    author, message = get_commit_info(commit_hash)
    update_changelog('CHANGELOG.md', author, message, commit_hash)
