defmodule NymServer.Repo.Migrations.ChangeNumVotesName do
  use Ecto.Migration

  def change do
    alter table(:ratings) do
      remove :numVotes
      add :num_votes, :float
    end
  end
end
