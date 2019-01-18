defmodule NymServer.RatingTest do
  use NymServer.ModelCase

  alias NymServer.Rating

  @valid_attrs %{domain: "some content", item: "some content", score: 42, num_votes: 42, nym_id: 1}
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = Rating.changeset(%Rating{}, @valid_attrs)
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = Rating.changeset(%Rating{}, @invalid_attrs)
    refute changeset.valid?
  end
end
