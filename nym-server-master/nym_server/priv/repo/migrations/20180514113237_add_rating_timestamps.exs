defmodule NymServer.Repo.Migrations.AddRatingTimestamps do
  use Ecto.Migration

  def change do
    alter table(:ratings) do
      add :inserted_at, :utc_datetime, default: fragment("NOW()")
      add :updated_at, :utc_datetime, default: fragment("NOW()")
    end
  end
end
