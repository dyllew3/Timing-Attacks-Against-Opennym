defmodule NymServer.RatingTest do
  use NymServer.ModelCase

  alias NymServer.Rating

  @valid_attrs %{domain: "some content", item: "some content", num_votes: 42, score: 42}
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
