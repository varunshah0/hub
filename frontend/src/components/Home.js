import { useNavigate, A } from "@solidjs/router";
import { createSignal, createEffect, onMount, Show } from "solid-js";
import { fetchUserData } from "../utils";
import { useStore } from "../store";
import Player from "./Player";

const Home = () => {
  const [store, { setLoggedIn, setData }] = useStore();

  createEffect(() => {
    if (!store.loggedIn) {
      const navigate = useNavigate();
      navigate("/login", { replace: true });
    }
  });

  onMount(() => {
    if (!store?.data?.username) {
      fetchUserData(setLoggedIn, setData);
    }
  });

  return (
    <div>
      <h1 class="text-4xl font-bold mb-4 text-red-500">
        Welcome {store?.data?.full_name || store?.data?.username}!
      </h1>
      <div>
        <Show
          when={!store.data.player}
          fallback={
            <div>
              <Player player={store.data.player} />
            </div>
          }
        >
          <h3 class="text-2xl font-bold mb-4">
            Want to play?{" "}
            <A
              href="/registration"
              class="font-medium text-blue-600 dark:text-blue-500 hover:underline"
            >
              Register!
            </A>
          </h3>
        </Show>
      </div>
    </div>
  );
};

export default Home;
