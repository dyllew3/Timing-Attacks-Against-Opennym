defmodule NymServer.Repo.Migrations.CreateRulesTable do
  use Ecto.Migration

  def change do
    create table(:rules) do
      add :domain, :string
      add :endpoint, :string
      add :rule, :string
      add :inserted_at, :utc_datetime, default: fragment("NOW()")
      add :updated_at, :utc_datetime, default: fragment("NOW()")
    end
  end
end
