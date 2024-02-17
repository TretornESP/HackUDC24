#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import datetime

# Define a function to convert epoch time to UTC text-based date
def epoch_to_utc_text(epoch_time):
    utc_time = datetime.datetime.fromtimestamp(epoch_time, datetime.UTC)
    return utc_time.strftime('%Y-%m-%d %H:%M:%S UTC')

def epoch_to_filename(epoch_time):
    utc_time = datetime.datetime.fromtimestamp(epoch_time, datetime.UTC)
    return utc_time.strftime('%Y_%m_%d_%H_%M_%S')

def argparse(json_str, html_template_path):
    # Parse the string into a json file
    json_obj = json.loads(json_str)

    screening_data = json_obj["screening"]
    checking_data = json_obj["checking"]
    commit_data = json_obj["git"]

    template_file_path = html_template_path
    try:
        with open(template_file_path, 'r') as template_file:
            template_content = template_file.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_file_path}' not found.")
        sys.exit(1)
    
    return (screening_data, checking_data, commit_data, template_content)

def populate_lX_checks(checks_list_lX, color):
    # Replace placeholders in the red box wrapper
    color_box_content = []
    for check in checks_list_lX:
        # Check if subtitle and code are not None
        if check["Auto-fix"]:
            mouseover_description = f'<div class="suggestion-icon">!<span class="suggestion-icon-text"><div class="text-wrapper">{'<br>'.join(check["Auto-fix"])}</div></span></div>'
        else:
            mouseover_description = ''
        
        color_box_content.append(f'''
        <div class="checkbox {color}">
            <div>
                <a href="{check['Documentation']}">{check['Check']}</a>: {check['Title']}
                {mouseover_description}
            </div>
            <hr>
            <div>
                <p>Location: {check['Location']}</p>
                <p>Suggestion: {check['Suggestion']}</p>
                {f'<p>Related code: {check["Subtitle"]}</p>' if check["Subtitle"] else ''}
                {f'<textarea readonly rows="3" class="related_code {color}">\n{'\n'.join(check['Code'])}</textarea>' if check["Code"] else ''}
            </div>
        </div>
        ''')
    return '\n'.join(color_box_content)

def generate_pie_table(screening_checkers):
    total_checks = sum(check["#"] for check in screening_checkers)

    pie_table = ["['Checker', 'Occurrences'],"]
    for check in screening_checkers:
        pie_table.append(f'[\'{check["Checker"]}\', {check["#"]}],')

    return '\n'.join(pie_table)

def process(json_str, html_template_path, reports_dir="."):
    (screening_data, checking_data, commit_data, html_template) = argparse(json_str, html_template_path)

    # Extract Analysis data
    checking_analysis = checking_data['Analysis']
    checking_elapsed_ms = checking_analysis['ElapsedMillis']
    checking_compiler_flags = checking_analysis['CompilerFlags']
    if checking_compiler_flags == '':
        checking_compiler_flags = '-'

    # Initialize lists for different levels of checks
    checks_list_l1 = []
    checks_list_l2 = []
    checks_list_l3 = []

    # Extract checks data
    checks = checking_data['Checks']
    for check in checks:
        # Extract common fields
        check_data = {
            "Check": check["Check"],
            "Location": check["Location"],
            "Title": check["Title"],
            "Suggestion": check["Suggestion"],
            "Auto-fix": check["Auto-fix"],
            "Documentation": check["Documentation"],
            "Subtitle": check["RelatedCodeList"]["Subtitle"] if check["RelatedCodeList"] else None,
            "Code": check["RelatedCodeList"]["Code"] if check["RelatedCodeList"] else None
        }
        # Extract additional fields based on level
        level = check["Level"]
        if level == "L1":
            checks_list_l1.append(check_data)
        elif level == "L2":
            checks_list_l2.append(check_data)
        elif level == "L3":
            checks_list_l3.append(check_data)
    
     # Extracting screening checkers data
    screening_checkers = []
    if "Ranking of Checkers" in screening_data:
        ranking_of_checkers = screening_data["Ranking of Checkers"]
        for checkers_list in ranking_of_checkers:
            for checker_data in checkers_list:
                check_data = {
                    "Checker": checker_data["Checker"],
                    "Level": checker_data["Level"],
                    "Priority": int(checker_data["Priority"][1:]),
                    "#": int(checker_data["#"]),
                    "Title": checker_data["Title"]
                }
                screening_checkers.append(check_data)

    # Parse commit data
    git_repository_name = commit_data["Repository"]["Name"]
    git_repository_url = commit_data["Repository"]["URL"]
    git_branch = commit_data["Branch"]
    git_commit_hash = commit_data["Commit"]["Hash"]
    git_commit_url = commit_data["Commit"]["URL"]
    git_author = commit_data["Author"]
    git_date_epoch = int(commit_data["Date"])
    git_message = commit_data["Message"]

    # Print or do whatever you want with the extracted data
    print("Elapsed Millis:", checking_elapsed_ms)
    print("Compiler Flags:", checking_compiler_flags)
    print("\nChecks Level 1:")
    for check in checks_list_l1:
        print(check)
    print("\nChecks Level 2:")
    for check in checks_list_l2:
        print(check)
    print("\nChecks Level 3:")
    for check in checks_list_l3:
        print(check)

    print("\nGit Repository Name:", git_repository_name)
    print("Git Repository URL:", git_repository_url)
    print("Git Branch:", git_branch)
    print("Git Commit Hash:", git_commit_hash)
    print("Git Commit URL:", git_commit_url)
    print("Git Author:", git_author)
    print("Git Date (Epoch):", git_date_epoch)
    print("Git Date (UTC):", epoch_to_utc_text(git_date_epoch))
    print("Git Message:", git_message)


    # Replace placeholders in the HTML template with the extracted data
    placeholders = {
        "$commit$": git_commit_hash,
        "$repository_url$": git_repository_url,
        "$repository$": git_repository_name,
        "$branch$": git_branch,
        "$commit_url$": git_commit_url,
        "$author$": git_author,
        "$date$": epoch_to_utc_text(git_date_epoch),
        "$message$": git_message,

        "$elapsed$": checking_elapsed_ms,
        "$flags$": checking_compiler_flags,

        "$checkboxes_red$":    populate_lX_checks(checks_list_l1, "red"),
        "$checkboxes_yellow$": populate_lX_checks(checks_list_l2, "yellow"),
        "$checkboxes_green$":  populate_lX_checks(checks_list_l3, "green"),

        "$pie_chart_data$": generate_pie_table(screening_checkers),
    }
    
    for placeholder, value in placeholders.items():
        html_template = html_template.replace(placeholder, str(value))
    
    filename = f"{epoch_to_filename(git_date_epoch)}"
    print(f"Writing to {reports_dir}/{filename}.html", flush=True)
    # Write the modified HTML template to a new file
    with open(f"{reports_dir}/{filename}.html", 'w') as f:
        f.write(html_template)
    
    return filename

# Execute the main function if the script is run directly
if __name__ == "__main__":
    # Read the JSON string from the command line
    json_str = sys.argv[1]
    html_template_path = sys.argv[2]

    # Open the json file
    with open(json_str, 'r') as file:
        json_str = file.read()

    process(json_str=json_str, html_template_path=html_template_path)