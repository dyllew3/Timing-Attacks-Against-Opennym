defmodule NymServer.TimingDefense do

  require Logger

  use Task, restart: :permanent

  def capacity() do
    20
  end

  def argmin(arr) do
    Enum.find_index(arr, fn x -> x === Enum.min(arr) end)
  end

  def async_task() do
    a = ConCache.update(:my_cache, "to_send", fn(old_value) ->
      # This function is isolated on a row level. Modifications such as update, put, delete,
      # on this key will wait for this function to finish.
      # Modifications on other items are not affected.
      # Reads are always dirty.

      info = case old_value do
        nil -> %{ active_traces: 0, active_users: 0, active_dummy: 0}
        val -> val
      end

        {:ok, %{ active_traces: info.active_traces + 1, active_users: info.active_users, active_dummy: info.active_dummy + 1}}
    end)

    if a === :ok do
      HTTPoison.put("https://localhost:4400/ratings/padding/", "", [{"content-type", "application/json"}], [hackney: [:insecure]])
      ConCache.update(:my_cache, "to_send", fn(old_value) ->
        # This function is isolated on a row level. Modifications such as update, put, delete,
        # on this key will wait for this function to finish.
        # Modifications on other items are not affected.
        # Reads are always dirty.
        {:ok, %{ active_traces: old_value.active_traces - 1, active_users: old_value.active_users, active_dummy: old_value.active_dummy - 1}}
      end)

    end

  end


  def start_link(arg) do
    Task.start_link(__MODULE__, :run, [arg])
  end

  def run(_) do
    # ...
    #Logger.debug(inspect(ConCache.get(:my_cache, "test")))
    count = ConCache.get(:my_cache, "test")
    # a = ConCache.update(:my_cache, "test", fn(old_value) ->
    #   # This function is isolated on a row level. Modifications such as update, put, delete,
    #   # on this key will wait for this function to finish.
    #   # Modifications on other items are not affected.
    #   # Reads are always dirty.
    #   counts = case old_value do
    #         nil -> %{active_dummy: 0, active_traces: 0, time_stamp: NaiveDateTime.utc_now}
    #         _ -> old_value
    #   end

    #   if counts.active_dummy + counts.active_traces < capacity() do
    #     {:ok, %{ active_dummy: counts.active_dummy + 1, active_traces: counts.active_traces, time_stamp: counts.time_stamp}}
    #   else
    #     {:error, ""}
    #   end
    # end)
    # if  a === :ok do
    #   ConCache.update(:my_cache, "dummy_req", fn(val) ->
    #     case val do
    #       nil -> {:ok, 1}
    #       _ -> {:ok, val + 1}
    #     end
    #   end)
    #   Task.async(fn ->
    #     HTTPoison.put("https://localhost:4400/ratings/padding/", "", [{"content-type", "application/json"}], [hackney: [:insecure]])
    #     ConCache.update(:my_cache, "test", fn(old_value) ->
    #       # This function is isolated on a row level. Modifications such as update, put, delete,
    #       # on this key will wait for this function to finish.
    #       # Modifications on other items are not affected.
    #       # Reads are always dirty.
    #       counts = case old_value do
    #             nil -> %{active_dummy: 0, active_traces: 0, time_stamp: NaiveDateTime.utc_now}
    #             _ -> old_value
    #       end
    #       {:ok, %{ active_dummy: counts.active_dummy - 1, active_traces: counts.active_traces, time_stamp: counts.time_stamp}}
    #     end)
    #   end)
    # else
    #   Logger.debug("Full")
    # end
    # Logger.debug(inspect(count))
    # count = ConCache.get(:my_cache, "test")
    #Logger.debug(argmin([2,3,4,5,1]))
    b = for times <- 1..11 do
      (times - 6)/5
    end

    p = 1000

    z_k = case ConCache.get(:my_cache, "zk") do
      nil -> 20
      val -> val
    end

    q = case ConCache.get(:my_cache, "queue") do
      nil -> 20
      val -> val
    end

    mins = Enum.map(b, fn x -> x * (0 - q*p) end)
    min_val = Enum.at(b, argmin(mins))

    next_z = cond do
      z_k + min_val  < 0 or  z_k + min_val  > capacity() -> 0
      Enum.at(Enum.to_list(mins), argmin(mins)) === Enum.at(Enum.to_list(mins), 5) -> z_k
      true -> z_k + min_val
    end

    current_state = case  ConCache.get(:my_cache, "to_send") do
      nil -> %{ active_traces: 0, active_users: 0, active_dummy: 0}
      val -> val
    end

    cond do
      next_z > current_state.active_traces -> Task.async(fn -> async_task() end)
      true -> 0
    end

    current_state = case  ConCache.get(:my_cache, "to_send") do
      nil -> %{ active_traces: 0, active_users: 0, active_dummy: 0}
      val -> val
    end

    #Logger.debug(inspect(current_state.active_traces))
    #Logger.debug(inspect(current_state.active_users))

    next_q_mid =  q + 1*(current_state.active_users*p -  current_state.active_traces*p)
    next_q = cond do
      next_q_mid >= 0 -> next_q_mid
      true -> 0

    end
    ConCache.put(:my_cache, "queue", next_q)
    ConCache.put(:my_cache, "zk", next_z)
    #ConCache.update(:my_cache, "to_send", fn(old_value) ->
    #  counts = case old_value do
    #    nil -> %{ active_traces: 0, active_users: 0, active_dummy: 0}
    #    val -> val
    #  end
    #    {:ok, %{ active_traces: old_value.active_users, active_users: old_value.active_users, active_dummy: old_value.active_dummy}}
    #end)
    :timer.sleep(500)
  end
end
