defmodule NymServer.RuleTest do
  use NymServer.ModelCase

  alias NymServer.Rule

  @valid_attrs %{domain: "some content", endpoint: "some content", rule: "some content"}
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = Rule.changeset(%Rule{}, @valid_attrs)
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = Rule.changeset(%Rule{}, @invalid_attrs)
    refute changeset.valid?
  end
end
