defmodule NymServer.Repo.Migrations.AddRatingArrayForNym do
  use Ecto.Migration

  def change do
    alter table(:nyms) do
      add :ratings, {:array, :id}
    end
  end
end
