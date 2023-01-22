# ara-flask

anime service built with flask and cockroachdb\* and hosted at https://ara-flask-production.up.railway.app/

\*actually just postgresql until cockroachdb issue is resolved

## Endpoints

### Anime object

| Field      | Desc                                     |
| ---------- | ---------------------------------------- |
| id         | integer, corresponds to MyAnimeList id   |
| title      | string                                   |
| synopsis   | string                                   |
| genre      | string[]                                 |
| aired      | string                                   |
| episodes   | integer                                  |
| members    | integer, number of lists that contain it |
| popularity | integer, lower is better                 |
| ranked     | integer, lower is better                 |
| score      | float, 0 to 5                            |
| img_url    | string                                   |
| link       | string                                   |

`GET /anime?id=<id>`

Returns Anime

`POST /anime`

Request body = Anime

Returns 204 on success

`POST /import?id=<id>`

No request body, information comes from MyAnimeList API

Returns 204 on success

`GET /rate`

Returns semi-random Anime for rating

`POST /rate`

Request body

```json
{
  id: <id>
  score: <score>
}
```

`GET /recent`

returns 10 most recent ratings

`GET /top?genre=<genre>`

Returns top 10 Anime of a genre by score

`GET /bot?genre=<genre>`

Returns top 10 Anime of a genre by score

`GET /recs?genre=<genre>`

Returns 10 randomly chosen Anime, biased torwards top rated anime in genre.

`GET /pick`

Returns 10 hard coded animes that we think are good.

`GET /search?query=<query>`

Returns a list of Anime whose title's fuzzy match the query.

## Bootstrap database

To initialize database with web scraped data, there is a shameful script that inserts rows.

```sh
python shame.py
```

Initialize tables

```sh
pqsl postgres_connection_url < dbinit.sql
```
