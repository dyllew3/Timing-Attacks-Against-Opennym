defmodule NymServer.RatingController do
  use NymServer.Web, :controller

  alias NymServer.{Nym, Rating, Rule}
  alias Ecto.{NoResultsError}

  import NymServer.Utils

  require Logger

  def index(conn, %{"nym_id" => nym_id, "domain" => domain}) do
    # Check nym exists and domain supported, then return nym
    nym_query =
      case {Repo.get(Nym, nym_id), Repo.get_by(Rule, [domain: domain])} do
        {nil, _} -> {:failed, :not_found}
        {_, nil} -> {:failed, :not_found}
        {nym, _} -> Repo.preload(nym, :ratings)
      end

    # Check if nym retrieved, send response
    case nym_query do
      {:failed, reason} -> error_response(conn, reason)
      nym -> ratings = filter_domains(nym.ratings, domain)
          |> Enum.sort_by(&(&1.score), &>=/2) # Sort in descending order by num votes
          |> Enum.take(10)

          conn
          |> assign(:ratings, ratings)
          |> render("index.json")
    end
  end

  # Get single rating item that matches given parameters
  def show(conn, %{"nym_id" => nym_id, "domain" => domain, "id" => id}) do
    try do
      rating = Repo.get_by!(Rating, [nym_id: nym_id, domain: domain, item: id])
      render(conn, "show.json", rating: rating)
    rescue
      # If rating doesn't exist, create it given valid nym ID and domain
      NoResultsError -> case {Repo.get(Nym, nym_id), Repo.get_by(Rule, [domain: domain])} do
        {nil, _} -> error_response(conn)
        {_, nil} -> error_response(conn)
        _        -> conn
                 |> assign(:rating, %Rating{domain: domain, item: id, score: 0.0, num_votes: 0, nym_id: nym_id})
                 |> render("show.json")
      end
    end
  end

  def update(conn, params) do
    rating_map = params["rating"]
    nym_rating = rating_map["nymRating"]

    # Get rating struct from db or create new one
    db_query =
      try do
        case Repo.get_by(Rating, [nym_id: rating_map["nym_id"], domain: rating_map["domain"], item: rating_map["item"]]) do
          nil     -> case {Repo.get(Nym, rating_map["nym_id"]), Repo.get_by(Rule, [domain: rating_map["domain"]])} do
                       {nil, _} -> {:failed, :not_found}
                       {_, nil} -> {:failed, :not_found}
                       _        -> %Rating{domain: rating_map["domain"], item: rating_map["item"], score: 0.0, num_votes: 0, nym_id: rating_map["nym_id"]}
                     end
          result  -> result
        end
      rescue
        ArgumentError -> {:failed, :bad_request}
      end

    # Only keep rating object if the update is sequential
    rating_object =
      case db_query do
        {:failed, reason} -> {:failed, reason}
        rating            ->
          case ((rating.num_votes + 1) == nym_rating["numVotes"]) do
            true -> rating
            false -> {:conflict, %{
              num_votes: rating.num_votes,
              score: rating.score
            }}
          end
      end

    # Try upserting struct
    insert_result =
      case rating_object do
        {:failed, reason} -> {:failed, reason}
        {:conflict, updated_rating} -> {:conflict, updated_rating}
        rating            -> changeset = Rating.changeset rating, %{num_votes: nym_rating["numVotes"], score: nym_rating["score"]}
                             Repo.insert_or_update changeset
      end

    # Handle response from upserting struct
    case insert_result do
      {:failed, reason} -> error_response(conn, reason)
      {:error, _}       -> error_response(conn, :internal_server_error)
      {:conflict, updated_rating} -> conn
                                  |> put_status(:conflict)
                                  |> assign(:updated_rating, updated_rating)
                                  |> render("conflict.json")
      {:ok, rating}     -> conn
                        |> assign(:rating, rating)
                        |> render("update.json")
    end
  end

  # Given list of rating objects, return only ratings from specified domain
  defp filter_domains([], _), do: []
  defp filter_domains([rating|t], match_domain) do
    case rating.domain do
      ^match_domain -> [rating | filter_domains(t, match_domain)]
      _      -> filter_domains(t, match_domain)
    end
  end
end
