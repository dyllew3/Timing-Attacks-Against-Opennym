defmodule NymServer.NymTest do
  use NymServer.ModelCase

  alias NymServer.Nym

  @valid_attrs %{name: "some content", nym_id: 1}
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = Nym.changeset(%Nym{}, @valid_attrs)
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = Nym.changeset(%Nym{}, @invalid_attrs)
    refute changeset.valid?
  end
end
