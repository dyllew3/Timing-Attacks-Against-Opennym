defmodule NymServer.Repo.Migrations.CreateNymMetadata do
  use Ecto.Migration

  def change do
    create table(:nym_metadata) do
      add :clustering_version, :float
    end
  end
end
