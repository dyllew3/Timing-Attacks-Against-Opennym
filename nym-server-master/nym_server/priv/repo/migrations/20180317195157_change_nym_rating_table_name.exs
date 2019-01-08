defmodule NymServer.Repo.Migrations.ChangeNymRatingTableName do
  use Ecto.Migration

  def change do
    alter table(:nyms) do
      remove :ratings
      add :top_ratings, {:array, :id}
    end
  end
end
