defmodule NymServer.Rule do
  use Ecto.Schema
  import Ecto.Changeset

  schema "rules" do
    field :domain, :string
    field :endpoint, :string
    field :rule, :string
    timestamps()
  end

  def changeset(rule, params \\ %{}) do
    rule
    |> cast(params, [:domain, :endpoint, :rule])
    |> validate_required([:domain, :endpoint, :rule])
  end
end
