from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from datetime import date
from time import sleep

def store_data(filename, data1, data2): # takes data, writes it to a file, returns the full file data
    current_date = get_date()
    f = open(filename, "a")
    f.write("{}\t\t\t\t{:,}\t\t\t\t\t{:,}".format(current_date, data1, data2))
    f.close()

def get_date():
    current_date = str(date.today())
    year, month, day = current_date.split("-")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i in range(1, 13):
        if month == "0"+str(i):
            month = months[i-1]
            break
        if month == str(i):
            month = months[i-1]
            break
    return f"\n{month} {day}, {year}"

def get_statistics():
    # set browser options
    options = Options()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")

    browser = webdriver.Chrome("chromedriver", options=options)
    browser.get("https://musescore.com/user/login?destination=%2F")
    browser.implicitly_wait(3)

    input("[.] Please log in. Once logged in, press ENTER to continue.")

    while browser.current_url != "https://musescore.com/dashboard":
        input("[!] Login failed. Please login again.")

    print("[+] Login successful")
    print("[+] Dashboard accessed")
    # get statistics
    browser.get('https://musescore.com/score/stats/user/index')
    print("[+] Statistics accessed")
    sleep(3)
    data = str(browser.page_source)
    data = data[data.index("<tbody>"):data.index("</tbody>")].split(sep='<td class="title-td">')[1:]
    browser.close()

    return data

def calculate_statistics(data):
    # organize data
    print("[+] Organizing data...")

    views = 0
    plays = 0
    downloads = 0
    comments = 0
    favourites = 0
    rating = 0
    num_ratings = 0
    votes = 0

    total_scores = len(data)
    for i in range(total_scores):
        score = data[i].split(sep='</td><td>')
        score[0] = score[0][score[0].index('">')+2:-4]
        score[9] = score[9][:score[9].index("<")]
        views += int(score[1])
        plays += int(score[2])
        downloads += int(score[3])
        comments += int(score[4])
        favourites += int(score[5])
        if score[8] != '0.0':
            rating += float(score[8])
            num_ratings += 1
        votes += int(score[9])
        data[i] = score

    # calculate data
    print("[+] Calculating data...")
    avg_views = round(views/total_scores, 1)
    avg_plays = round(plays/total_scores, 1)
    avg_downloads = round(downloads/total_scores, 1)
    avg_comments = round(comments/total_scores, 1)
    avg_favourites = round(favourites/total_scores, 1)
    avg_rating = round(rating/num_ratings, 1)
    avg_votes = round(votes/total_scores, 1)

    return [views, plays, downloads, comments, favourites, votes, avg_views, avg_plays, avg_downloads, avg_comments, avg_favourites, avg_rating, avg_votes]

def output_statistics(statistics):
    views, plays, downloads, comments, favourites, votes, avg_views, avg_plays, avg_downloads, avg_comments, avg_favourites, avg_rating, avg_votes = statistics
    print("[?] Choose an output:")
    print("1) Print statistics to console")
    print("2) Write statistics to files")
    choice = input("Choose an output: ")
    while choice != "1" and choice != "2":
        choice = input("[!] Invalid input. Enter again:")

    current_date = get_date()
    if choice == "1":
    # print data
        print("\n\nYour MuseScore statistics as of: {}".format(current_date[1:]))
        print("\t\t\t\tTOTAL:\t\t\tAVERAGE PER SCORE:")
        stats_names = ['Views:    ', 'Plays:    ', 'Downloads:', 'Comments:', 'Favourites:']
        stats = [views, plays, downloads, comments, favourites]
        averages = [avg_views, avg_plays, avg_downloads, avg_comments, avg_favourites]
        for i in range(5):
            print("{}\t\t\t{:,}\t\t\t{:,}".format(stats_names[i], stats[i], averages[i]))

        print("Ratings:\t\t\t{:,}\t\t\t{:,}".format(votes, avg_votes))
    else:
        # store data
        print("[+] Saving data...")
        stats_names = ['views.txt', 'plays.txt', 'downloads.txt', 'comments.txt', 'favourites.txt']
        stats = [views, plays, downloads, comments, favourites]
        averages = [avg_views, avg_plays, avg_downloads, avg_comments, avg_favourites]
        for i in range(5):
            store_data(stats_names[i], stats[i], averages[i])

        # store ratings
        f = open("ratings.txt", "a")
        f.write("{}\t\t\t\t{:,}\t\t\t\t{:,}\t\t\t\t{:,}".format(current_date, votes, avg_votes, avg_rating))
        f.close()

        print("[+] Done.")


if __name__ == "__main__":
    data = get_statistics()
    statistics = calculate_statistics(data)
    output_statistics(statistics)