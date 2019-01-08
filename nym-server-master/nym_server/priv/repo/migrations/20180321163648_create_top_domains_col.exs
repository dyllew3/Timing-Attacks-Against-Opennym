defmodule NymServer.Repo.Migrations.CreateTopCookiesCol do
  use Ecto.Migration

  def change do
    alter table(:nyms) do
      add :top_domains, {:array, :string}
    end
  end
end
