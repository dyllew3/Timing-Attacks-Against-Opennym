defmodule NymServer.CookieTest do
  use NymServer.ModelCase

  alias NymServer.SessionCookies

  @valid_attrs %{cookies: "some content", domain: "some content", nym_id: 1}
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = SessionCookies.changeset(%SessionCookies{}, @valid_attrs)
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = SessionCookies.changeset(%SessionCookies{}, @invalid_attrs)
    refute changeset.valid?
  end
end
