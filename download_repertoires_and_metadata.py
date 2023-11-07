import os
os.environ['GEVENT_SUPPORT'] = 'True'
from collect import collect_repertoires_and_count_rearrangements, download_study
import pandas as pd

#outdir = r"C:\Users\yaniv\Desktop\yaarilab-genotype_tool-b11f598b9e93\yaarilab-genotype_tool-b11f598b9e93\downloads"

default_repository_df = pd.DataFrame(
    [
        'https://covid19-1.ireceptor.org',
        'https://covid19-2.ireceptor.org',
        'https://covid19-3.ireceptor.org',
        'https://covid19-4.ireceptor.org',
        'https://ipa1.ireceptor.org',
        'https://ipa2.ireceptor.org',
        'https://ipa3.ireceptor.org',
        'https://ipa4.ireceptor.org',
        'https://ipa5.ireceptor.org',
        'https://ipa6.ireceptor.org',
        'https://vdjserver.org',
        'https://scireptor.dkfz.de',
        'https://airr-seq.vdjbase.org',
        'https://roche-airr.ireceptor.org',
        'https://t1d-1.ireceptor.org',
        'https://agschwab.uni-muenster.de'
    ], columns=['URL']
)


def get_repositories():
    stop_loop = False
    print("Available repositories:")
    for idx, url in enumerate(default_repository_df['URL'], 1):
        print(f"{idx}. {url}")

    while not stop_loop:
        valid_input = True

        selected_indices = input(
            "Enter the indices of the repositories you want to download from (e.g., 1 2 3): ").split()
        for number in selected_indices:
            if int(number) < 1 or int(number) > len(default_repository_df):
                print(f"{number} is not in the range")
                valid_input = False

        if valid_input:
            stop_loop = True

    selected_urls = [default_repository_df['URL']
                     [int(idx) - 1] for idx in selected_indices]
    # Create DataFrame from selected URLs
    selected_repository_df = pd.DataFrame(selected_urls, columns=['URL'])
    return selected_repository_df


def main():
    outdir = input("Please enter the path to download to.")
    while True:
        if not os.path.isdir(outdir):
                os.makedirs(outdir)
        study_id = input("Enter study ID, or exit to finish: ")
        if study_id == "exit":
            return
        selected_repository_df = get_repositories()
        print("Sending search request...")
        search_results = collect_repertoires_and_count_rearrangements(
            selected_repository_df, study_id)

        if len(search_results['Repertoire']) > 0:
            print(f"Found {len(search_results['Repertoire'])} repertoires.")
            print("Sending download request...")
            download_results = download_study(study_id, search_results['Repertoire'], outdir)
            if download_results:
                print(
                    f"Download initiated. Downloader ID: {download_results['downloader_id']}")
            else:
                print(
                    f"Error in download process: {download_results.get('error', 'Unknown error')}")
        else:
            print(f"Error in search process or no repertoires found")


if __name__ == "__main__":
    main()