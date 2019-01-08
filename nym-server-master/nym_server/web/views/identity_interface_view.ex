defmodule NymServer.IdentityInterfaceView do
  use NymServer.Web, :view

  # Render list of rating objects
  def render("domain_index.json", %{ratings: ratings}) do
    ratings = Enum.map(ratings, &render_rating/1)
    %{
      ratings: ratings
    }
  end

  # Render Rating object as json
  defp render_rating(rating) do
    %{
      rating: %{
        domain: rating.domain,
        item: rating.item,
        nymRating: %{
          score: rating.score,
          numVotes: rating.num_votes
        },
        timestamp: rating.updated_at,
        nym: rating.nym_id
      }
    }
  end
end

