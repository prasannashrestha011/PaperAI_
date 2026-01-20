import Providers from "@/app/providers";
import SessionView from "@/components/SessionView";

type Params = Promise<{ id: string }>;

const Page = async (props: { params: Params }) => {
  const params = await props.params;
  const id = params.id;

  return (
    <div>
      <Providers>

      <SessionView doc_id={id}/>
      </Providers>
    </div>
  )
}

export default Page