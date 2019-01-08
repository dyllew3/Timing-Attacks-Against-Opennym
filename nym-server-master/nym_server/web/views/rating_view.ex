defmodule NymServer.RatingView do
  use NymServer.Web, :view

  # Render list of rating objects
  def render("index.json", %{ratings: ratings}) do
    ratings = Enum.map(ratings, &render_rating/1)
    %{
      ratings: ratings
    }
  end

  # Render single rating object
  def render("show.json", %{rating: rating}) do
    render_rating(rating)
  end

  def render("update.json", %{rating: rating}) do
      %{
        result: render_rating(rating)
      }
  end

  def render("conflict.json", %{updated_rating: updated_rating}) do
    %{
      result: %{
        numVotes: updated_rating.num_votes,
        score: updated_rating.score
      }
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
        }
      }
    }
  end
end
