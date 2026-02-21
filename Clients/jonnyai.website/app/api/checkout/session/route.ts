import { NextResponse } from "next/server";
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY as string, {
  apiVersion: "2026-01-28.clover",
});

export async function POST(req: Request) {
  try {
    const { amount, planName } = await req.json();

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      line_items: [
        {
          price_data: {
            currency: "gbp",
            product_data: {
              name: `JonnyAI Service: ${planName}`,
              description: "Phase 1: Deep Scoping & Rapid Prototype",
            },
            unit_amount: amount * 100, // Stripe expects pence
          },
          quantity: 1,
        },
      ],
      mode: "payment",
      success_url: `${new URL(req.url).origin}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${new URL(req.url).origin}/pricing`,
    });

    return NextResponse.json({ id: session.id, url: session.url });
  } catch (err: any) {
    console.error("Stripe Session Error:", err);
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
