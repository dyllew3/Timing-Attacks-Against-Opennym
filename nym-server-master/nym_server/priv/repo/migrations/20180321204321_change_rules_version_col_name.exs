defmodule NymServer.Repo.Migrations.ChangeRulesVersionColName do
  use Ecto.Migration

  def change do
    alter table(:nym_metadata) do
      remove :rules_version
      add :support_list_version, :float
    end
  end
end
