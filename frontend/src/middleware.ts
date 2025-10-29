import { authMiddleware } from '@clerk/nextjs'

export default authMiddleware({
  // Routes that can be visited while signed out
  publicRoutes: ['/sign-in(.*)', '/sign-up(.*)'],
  // Routes that can always be visited
  // afterAuth(auth, req, evt) {
  //   // Handle users who aren't authenticated
  //   if (!auth.userId && !auth.isPublicRoute) {
  //     return redirectToSignIn({ returnBackUrl: req.url })
  //   }
  // }
})

export const config = {
  matcher: ["/((?!.+\\.[\\w]+$|_next).*)", "/", "/(api|trpc)(.*)"],
}