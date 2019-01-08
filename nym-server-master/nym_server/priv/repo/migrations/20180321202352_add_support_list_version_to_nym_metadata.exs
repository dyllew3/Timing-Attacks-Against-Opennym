defmodule NymServer.Repo.Migrations.AddSupportListVersionToNymMetadata do
  use Ecto.Migration

  def change do
    alter table(:nym_metadata) do
      add :rules_version, :float
    end
  end
end
