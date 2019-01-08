defmodule NymServer.Repo.Migrations.CreateRating do
  use Ecto.Migration

  def change do
    create table(:ratings) do
      add :domain, :string
      add :item, :string
      add :score, :float
      add :numVotes, :integer
      add :nym_id, references(:nyms)
    end
  end
end
