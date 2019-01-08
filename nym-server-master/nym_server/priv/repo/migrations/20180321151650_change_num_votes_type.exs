defmodule NymServer.Repo.Migrations.ChangeNumVotesType do
  use Ecto.Migration

  def change do
    alter table(:ratings) do
      modify :num_votes, :integer
    end
  end
end
