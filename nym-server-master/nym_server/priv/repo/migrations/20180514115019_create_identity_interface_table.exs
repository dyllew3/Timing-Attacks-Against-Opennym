defmodule NymServer.Repo.Migrations.CreateIdentityInterfaceTable do
  use Ecto.Migration

  def change do
    create table(:identity_interface) do
      add :domain, :string
      add :username, :string
      add :nym_id, :integer
      add :inserted_at, :utc_datetime, default: fragment("NOW()")
      add :updated_at, :utc_datetime, default: fragment("NOW()")
    end
  end
end
