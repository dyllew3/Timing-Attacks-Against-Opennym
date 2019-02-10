defmodule NymServer.NymController do
    use NymServer.Web, :controller

    alias NymServer.{Nym, Rating, NymMetadata}
    import NymServer.Utils

    # Returns all Nyms
    def index(conn, _params) do
      case Repo.all Nym do
        []   -> conn
              |> error_response(:not_found)
        nyms -> conn
              #|> assign(:nyms, Enum.map(nyms, &insert_nym_ratings/1))
              |> register_before_send(&pad_packet(&1))
              |> send_resp(200, Poison.encode! %{nyms: Enum.map(nyms, &insert_nym_ratings/1) })
              #|> render("index.json")


      end
    end

    # Returns one Nym as identified by ID
    def show(conn, %{"id" => id}) do
      case Repo.get(Nym, id) do
        nil -> conn
             |> error_response(:not_found)
        nym -> conn
             #|> assign(:nym, insert_nym_ratings(nym))
             #|> render("show.json")
             |> register_before_send(&pad_packet(&1))
             |> send_resp(200, Poison.encode! insert_nym_ratings(nym))

      end
    end

    # def version_index(conn, _params) do
    #   case Repo.one NymMetadata do
    #     nil -> conn
    #         |> put_status(:not_found)
    #         |> text("")
    #     nym_metadata -> conn
    #         |> assign(:clustering_version, nym_metadata.clustering_version)
    #         |> render("version_index.json")
    #   end
    # end

    # Given a Nym, return a map containing the Nym and it's ratings
    defp insert_nym_ratings(nym) do
      top_ratings = Enum.map(nym.top_ratings, &get_rating/1)
      %{
        id: nym.id,
        topRatings: top_ratings,
        topDomains: nym.top_domains
      }
    end

    # Get a rating from it's ID
    defp get_rating(id) do
      Repo.get(Rating, id) |> generate_rating
    end

    # Create a Map Representation of a Rating
    defp generate_rating(rating) do
      %{
        rating: %{
          domain: rating.domain,
          item: rating.item,
          nymRating: %{
            score: rating.score,
            numVotes: rating.num_votes
          }
        }
      }
    end
end
