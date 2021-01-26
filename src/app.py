from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def Diff(li1, li2):
    return list(list(set(li1) - set(li2)) + list(set(li2) - set(li1)))


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/github-followers", methods=["GET", "POST"])
def github_followers():
    if request.method == "POST":
        username = request.form["username"]
        try:
            total_followers_following_req = requests.get(
                f"https://api.github.com/users/{username}"
            )

            total_followers = total_followers_following_req.json()["followers"]
            followers = []

            total_following = total_followers_following_req.json()["following"]
            following = []

            for page in range(total_followers // 100 + 1):
                followers_req = requests.get(
                    f"https://api.github.com/users/{username}/followers?page={page+1}&per_page=100"
                )

                for follower in followers_req.json():
                    followers.append(follower["html_url"])

            for page in range(total_followers // 100 + 1):
                following_req = requests.get(
                    f"https://api.github.com/users/{username}/following?page={page+1}&per_page=100"
                )
                for follow in following_req.json():
                    following.append(follow["html_url"])

            followers_diff = Diff(followers, following)

            return render_template("index.html", followers_diff=followers_diff)
            
        except:
            return render_template("rate_limit.html")
    else:
        return render_template("index.html")
