from flask import Flask, jsonify, request

from storage import all_articles, liked_articles, not_liked_articles, did_not_watch
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)

@app.route("/get-article")
def get_article():
    article_data = {
        "title": all_articles[0][10],
        "event_type": all_articles[0][1]
    }
    return jsonify({
        "data": article_data,
        "status": "success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    article = all_articles[0]
    not_liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201


@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "title": article[10],
            "event_type": article[1],
            "language": article[12],
            "text": article[11]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "event_type": recommended[1],
            "language": recommended[2],
            "text": recommended[3]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)