defmodule NymServer.CookieTest do
  use NymServer.ModelCase

  alias NymServer.Cookie

  @valid_attrs %{cookie: "some content", domain: "some content"}
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = Cookie.changeset(%Cookie{}, @valid_attrs)
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = Cookie.changeset(%Cookie{}, @invalid_attrs)
    refute changeset.valid?
  end
end
