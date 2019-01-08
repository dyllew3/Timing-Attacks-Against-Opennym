defmodule NymServer.Repo.Migrations.CreateNym do
  use Ecto.Migration

  def change do
    create table(:nyms, primary_key: false) do
      add :id, :id, primary_key: true

    end
  end
end
