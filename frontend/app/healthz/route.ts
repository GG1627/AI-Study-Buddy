export async function GET() {
  return Response.json({
    status: "healthy",
    service: "SurgiTrack Frontend",
    timestamp: new Date().toISOString(),
  });
}
